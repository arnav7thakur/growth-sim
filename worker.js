export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path.startsWith("/marketing-growth-sim")) {
      const targetUrl = "https://growth-sim.streamlit.app" + path.replace("/marketing-growth-sim", "");

      const reqInit = {
        method: request.method,
        headers: request.headers,
        redirect: "follow",
      };

      if (request.method !== "GET" && request.method !== "HEAD") {
        reqInit.body = await request.clone().arrayBuffer();  // Clone + read body safely
      }

      const response = await fetch(targetUrl, reqInit);

      const newHeaders = new Headers(response.headers);
      newHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    return new Response("Not found", { status: 404 });
  }
}
