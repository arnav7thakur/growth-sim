export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path.startsWith("/marketing-growth-sim")) {
      const targetUrl = "https://growth-sim.streamlit.app" + path.replace("/marketing-growth-sim", "");

      const init = {
        method: request.method,
        headers: request.headers,
        redirect: "follow",
      };

      // Only include body if it's a method that supports it
      if (request.method !== "GET" && request.method !== "HEAD") {
        init.body = request.body;
      }

      const response = await fetch(targetUrl, init);

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
