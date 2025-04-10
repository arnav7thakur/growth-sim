export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path.startsWith("/marketing-growth-sim")) {
      const targetUrl = "https://growth-sim.streamlit.app" + path.replace("/marketing-growth-sim", "");

      const modifiedRequest = new Request(targetUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
        redirect: "follow",
      });

      // Use fetch to proxy content without redirecting user
      const response = await fetch(modifiedRequest);

      // Clone and modify CORS headers if needed
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
