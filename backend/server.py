import cv2
import numpy as np
import psutil
import platform
import json
from aiohttp import web
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
    RTCDataChannel,
)
from av import VideoFrame
from os import getenv
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemMonitor:
    def __init__(self):
        self.has_gpu = self._check_gpu_availability()

    def _check_gpu_availability(self):
        try:
            import subprocess

            subprocess.check_output(["nvidia-smi"])
            return True
        except:
            return False

    def get_system_info(self):
        """システムリソース情報の取得"""
        info = {
            "timestamp": time.time(),
            "cpu": {
                "total": psutil.cpu_percent(interval=None),
                "per_cpu": psutil.cpu_percent(interval=None, percpu=True),
                "memory": psutil.virtual_memory().percent,
            },
        }

        if self.has_gpu:
            try:
                import subprocess

                cmd = "nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits"
                output = subprocess.check_output(cmd.split(), universal_newlines=True)
                util, mem_used, mem_total = output.strip().split(",")

                info["gpu"] = {
                    "utilization": float(util),
                    "memory_used": float(mem_used),
                    "memory_total": float(mem_total),
                }
            except Exception as e:
                logger.error(f"GPU info error: {str(e)}")

        return info


class VideoProcessor:
    def __init__(self):
        # カスケード分類器の初期化（例：顔検出）
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.processing_mode = "original"  # 初期モード
        self.available_modes = ["original", "gray", "edge", "face_detect"]

    def process_frame(self, frame):
        if self.processing_mode == "original":
            return frame
        elif self.processing_mode == "gray":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif self.processing_mode == "edge":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        elif self.processing_mode == "face_detect":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return frame
        return frame

    def set_mode(self, mode):
        if mode in self.available_modes:
            self.processing_mode = mode
            return True
        return False


class VideoTransformTrack(VideoStreamTrack):
    def __init__(self, track, processor):
        super().__init__()
        self.track = track
        self.processor = processor

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")

        # 画像処理の実行
        processed_img = self.processor.process_frame(img)

        # 処理済み画像をフレームに変換
        new_frame = VideoFrame.from_ndarray(processed_img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame


class WebRTCServer:
    def __init__(self):
        self.pcs = set()
        self.system_monitor = SystemMonitor()
        self.video_processor = VideoProcessor()
        self.app = web.Application(middlewares=[self.cors_middleware])
        self.init_routes()

    @web.middleware
    async def cors_middleware(self, request, handler):
        headers = {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": getenv("CORS_ALLOW_ORIGIN", "*"),
        }
        # Respond immediately to OPTIONS requests with CORS headers
        if request.method == "OPTIONS":
            return web.Response(headers=headers)
        try:
            # Handle the request and set CORS headers on the response
            response = await handler(request)
            if isinstance(response, web.StreamResponse):
                for key, value in headers.items():
                    response.headers[key] = value
            return response
        except web.HTTPException as e:
            for key, value in headers.items():
                e.headers[key] = value
            raise e

    def init_routes(self):
        self.app.router.add_post("/offer", self.handle_offer)
        self.app.router.add_get(
            "/system_info", self.handle_system_info_sse
        )  # SSEルート追加

    async def handle_system_info_sse(self, request):
        """SSEでシステム情報を送信するエンドポイント"""
        response = web.StreamResponse(
            headers={"Content-Type": "text/event-stream", "Cache-Control": "no-cache"}
        )
        await response.prepare(request)

        while True:
            info = self.system_monitor.get_system_info()
            await response.write(
                f"data: {json.dumps({'type': 'system_info', 'data': info})}\n\n".encode()
            )
            await asyncio.sleep(1)  # 1秒間隔で送信

        return response

    async def handle_offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        # データチャネルの設定
        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                try:
                    data = json.loads(message)
                    if data["type"] == "set_mode":
                        success = self.video_processor.set_mode(data["mode"])
                        channel.send(
                            json.dumps(
                                {
                                    "type": "mode_change",
                                    "success": success,
                                    "current_mode": self.video_processor.processing_mode,
                                }
                            )
                        )
                except Exception as e:
                    logger.error(f"Error handling message: {str(e)}")

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            if pc.connectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        @pc.on("track")
        def on_track(track):
            if track.kind == "video":
                local_video = VideoTransformTrack(track, self.video_processor)
                pc.addTrack(local_video)

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.json_response(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        )

    async def cleanup(self, app):
        coros = [pc.close() for pc in self.pcs]
        await asyncio.gather(*coros)
        self.pcs.clear()

    def run(self):
        self.app.on_cleanup.append(self.cleanup)
        web.run_app(self.app, port=8080)


if __name__ == "__main__":
    server = WebRTCServer()
    server.run()
