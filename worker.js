export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Only proxy if path starts with /marketing-growth-sim
    if (path.startsWith("/marketing-growth-sim")) {
      const targetUrl = "https://growth-sim.streamlit.app" + path.replace("/marketing-growth-sim", "");
      return fetch(targetUrl, request);
    }

    return new Response("Not found", { status: 404 });
  }
}
