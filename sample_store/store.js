// Tiny cart stored in the browser (localStorage). No backend: this is the "before" store.
const PRODUCTS = [
  { id: "lavender", name: "Lavender Calm Candle", price: 24.0, note: "Hand-poured soy, 40h burn" },
  { id: "cedar", name: "Cedar & Smoke Candle", price: 28.0, note: "Woody, warm, 45h burn" },
  { id: "gift-set", name: "Cozy Night Gift Set", price: 89.0, note: "3 candles + matches" },
];

function getCart() {
  try { return JSON.parse(localStorage.getItem("cart") || "[]"); } catch { return []; }
}
function saveCart(cart) { localStorage.setItem("cart", JSON.stringify(cart)); }
function addToCart(id) {
  const cart = getCart();
  const line = cart.find((l) => l.id === id);
  if (line) line.qty += 1; else cart.push({ id, qty: 1 });
  saveCart(cart);
  document.getElementById("cart-count").textContent = cartCount();
}
function cartCount() { return getCart().reduce((n, l) => n + l.qty, 0); }
function cartTotal() {
  return getCart().reduce((sum, l) => sum + PRODUCTS.find((p) => p.id === l.id).price * l.qty, 0);
}
