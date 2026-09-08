import time
from typing import Dict, List, Any
from playwright.sync_api import Page

class MetricsInterceptor:
    def __init__(self):
        self.requests: List[Dict[str, Any]] = []
        self.pending_requests: Dict[str, float] = {}
        self.failed_requests: int = 0
        self.total_bytes: int = 0
        
    def attach(self, page: Page):
        page.on("request", self._on_request)
        page.on("response", self._on_response)
        page.on("requestfailed", self._on_request_failed)

    def _on_request(self, request):
        self.pending_requests[request.url] = time.perf_counter()

    def _on_response(self, response):
        start_time = self.pending_requests.pop(response.url, None)
        duration_ms = (time.perf_counter() - start_time) * 1000 if start_time else None
        
        body_bytes = int(response.headers.get("content-length", 0))
        self.total_bytes += body_bytes

        self.requests.append({
            "url": response.url,
            "status": response.status,
            "duration_ms": duration_ms,
            "size_bytes": body_bytes
        })

    def _on_request_failed(self, request):
        self.pending_requests.pop(request.url, None)
        self.failed_requests += 1

    def get_w3c_timings(self, page: Page) -> Dict[str, Any]:
        return page.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0];
            if (!nav) return {};
            return {
                ttfb_ms: nav.responseStart - nav.requestStart,
                dom_interactive_ms: nav.domInteractive - nav.startTime,
                load_event_ms: nav.loadEventEnd - nav.startTime
            };
        }""")