export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname.startsWith("/marketing-growth-sim")) {
      const target = "https://growth-sim.streamlit.app" + url.pathname.replace("/marketing-growth-sim", "");

      const init = {
        method: request.method,
        headers: request.headers,
        body: ["GET", "HEAD"].includes(request.method) ? undefined : await request.clone().arrayBuffer(),
      };

      const response = await fetch(target, init);
      const headers = new Headers(response.headers);
      headers.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    }

    return new Response("Not found", { status: 404 });
  }
}
