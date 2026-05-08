// Shared auth & security module — loaded on every protected page (after api.js)

// ── 1. Cache-Prevention Meta Tags ────────────────────────────────────────────
// Tells the browser not to cache this page, so a cached version
// can't be shown after logout.
(function () {
  [
    ["Cache-Control", "no-cache, no-store, must-revalidate"],
    ["Pragma",        "no-cache"],
    ["Expires",       "0"]
  ].forEach(function (pair) {
    var m = document.createElement("meta");
    m.setAttribute("http-equiv", pair[0]);
    m.setAttribute("content",    pair[1]);
    document.head.appendChild(m);
  });
}());

// ── 2. requireAuth ────────────────────────────────────────────────────────────
// Call this at the top of every protected page script.
// Returns the token string if logged in, or null (page redirects to login).
//
// Uses .replace() instead of .href so the protected page is REMOVED
// from browser history — pressing Back from login won't return here.
function requireAuth() {
  var token = localStorage.getItem("token");
  if (!token) {
    window.location.replace("login.html");
    return null;
  }
  return token;
}

// ── 3. logout ─────────────────────────────────────────────────────────────────
// Single shared logout used by every page.
// Clears ALL localStorage (token + exam data) then redirects.
function logout() {
  localStorage.clear();
  sessionStorage.clear();
  window.location.replace("login.html");
}

// ── 4. Back-Button / bfcache Protection ──────────────────────────────────────
// When the user presses Back, the browser often restores the page from its
// back/forward cache (bfcache) without re-running the top-level script.
// This "pageshow" listener fires in that case and re-checks the token.
window.addEventListener("pageshow", function (event) {
  if (event.persisted && !localStorage.getItem("token")) {
    window.location.replace("login.html");
  }
});

// ── 5. Tab-Visibility Protection ──────────────────────────────────────────────
// If the user logs out in another tab and then switches back to this tab,
// this listener re-checks auth and redirects if the token is gone.
document.addEventListener("visibilitychange", function () {
  if (document.visibilityState === "visible" && !localStorage.getItem("token")) {
    window.location.replace("login.html");
  }
});
