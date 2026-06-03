const WHATSAPP_NUMBER = "237657901106"; // Numero WhatsApp au format international, sans +.

const products = [
  {
    id: "snuffle-mat",
    name: "Tapis de fouille pour chien",
    category: "Animaux",
    icon: "🐶",
    description: "Produit emotionnel et demonstrable : le chien cherche ses croquettes, se calme et s'occupe.",
    price: 29.9,
    cost: 10.5,
    score: 96,
    colors: ["#bbf7d0", "#38bdf8"],
  },
  {
    id: "pet-bottle",
    name: "Gourde portable anti-fuite",
    category: "Animaux",
    icon: "💧",
    description: "Parfaite pour promenades, voyages et sorties. Achat impulsif facile à montrer en Reel.",
    price: 24.9,
    cost: 7.8,
    score: 94,
    colors: ["#bfdbfe", "#22c55e"],
  },
  {
    id: "car-seat-cover",
    name: "Protection siege voiture chien",
    category: "Voiture",
    icon: "🚗",
    description: "Resout un vrai probleme : poils, griffes et salete dans la voiture.",
    price: 39.9,
    cost: 17.5,
    score: 92,
    colors: ["#bae6fd", "#64748b"],
  },
  {
    id: "lint-remover",
    name: "Brosse anti-poils reutilisable",
    category: "Maison",
    icon: "✨",
    description: "Demo avant/apres tres forte pour canapes, tapis, vetements et sieges auto.",
    price: 19.9,
    cost: 5.4,
    score: 91,
    colors: ["#fde68a", "#38bdf8"],
  },
  {
    id: "mini-car-vacuum",
    name: "Mini aspirateur voiture USB",
    category: "Voiture",
    icon: "🧹",
    description: "Gadget visuel qui marche bien en contenu : miettes, poussiere, siege, coffre.",
    price: 34.9,
    cost: 16.2,
    score: 89,
    colors: ["#ddd6fe", "#60a5fa"],
  },
  {
    id: "cable-organizer",
    name: "Organisateur cables voyage",
    category: "Voyage",
    icon: "🔌",
    description: "Petit prix, faible risque SAV, utile pour etudiants, pros et voyageurs.",
    price: 18.9,
    cost: 4.6,
    score: 87,
    colors: ["#fed7aa", "#22c55e"],
  },
  {
    id: "compression-bags",
    name: "Sacs compression voyage",
    category: "Voyage",
    icon: "🧳",
    description: "Gain de place visible en video. Bon produit panier moyen avec lots.",
    price: 27.9,
    cost: 9.2,
    score: 86,
    colors: ["#fecaca", "#38bdf8"],
  },
  {
    id: "fridge-boxes",
    name: "Boites rangement frigo",
    category: "Maison",
    icon: "🥗",
    description: "Produit organisation maison, tres compatible avec contenus avant/apres.",
    price: 26.9,
    cost: 8.8,
    score: 85,
    colors: ["#d9f99d", "#93c5fd"],
  },
  {
    id: "electric-clean-brush",
    name: "Brosse nettoyage electrique",
    category: "Maison",
    icon: "🫧",
    description: "Produit demo fort pour joints, salle de bain, cuisine et taches visibles.",
    price: 32.9,
    cost: 14.5,
    score: 84,
    colors: ["#e0e7ff", "#22c55e"],
  },
  {
    id: "magnetic-phone-holder",
    name: "Support telephone voiture",
    category: "Voiture",
    icon: "📱",
    description: "Accessoire pratique, livraison facile, bon en upsell avec produits auto.",
    price: 17.9,
    cost: 4.2,
    score: 82,
    colors: ["#c4b5fd", "#38bdf8"],
  },
  {
    id: "slow-feeder",
    name: "Gamelle anti-glouton",
    category: "Animaux",
    icon: "🥣",
    description: "Produit animalier avec probleme clair : ralentir les repas trop rapides.",
    price: 22.9,
    cost: 6.7,
    score: 81,
    colors: ["#bbf7d0", "#fbbf24"],
  },
  {
    id: "drawer-dividers",
    name: "Separateurs tiroirs ajustables",
    category: "Maison",
    icon: "📦",
    description: "Produit rangement simple, léger et parfait pour videos organisation.",
    price: 21.9,
    cost: 6.1,
    score: 79,
    colors: ["#bae6fd", "#86efac"],
  },
];

let activeFilter = "all";
let cart = JSON.parse(localStorage.getItem("milostore-cart") || "{}");

const productGrid = document.querySelector("#product-grid");
const cartPanel = document.querySelector("#cart-panel");
const overlay = document.querySelector("#overlay");
const cartItems = document.querySelector("#cart-items");
const cartCount = document.querySelector("#cart-count");
const cartTotal = document.querySelector("#cart-total");
const whatsappOrder = document.querySelector("#whatsapp-order");

function formatPrice(value) {
  return `${value.toFixed(2).replace(".", ",")}€`;
}

function saveCart() {
  localStorage.setItem("milostore-cart", JSON.stringify(cart));
}

function getCartEntries() {
  return Object.entries(cart)
    .map(([id, quantity]) => {
      const product = products.find((item) => item.id === id);
      return product ? { ...product, quantity } : null;
    })
    .filter(Boolean);
}

function renderProducts() {
  const visibleProducts =
    activeFilter === "all" ? products : products.filter((item) => item.category === activeFilter);

  productGrid.innerHTML = visibleProducts
    .map((product) => {
      const margin = product.price - product.cost;
      return `
        <article class="product-card">
          <div class="product-art" style="--art-a:${product.colors[0]};--art-b:${product.colors[1]}">
            <span class="score">Score ${product.score}/100</span>
            <span class="product-icon" aria-hidden="true">${product.icon}</span>
          </div>
          <div class="product-body">
            <span class="category">${product.category}</span>
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <div class="price-line">
              <span class="price">${formatPrice(product.price)}</span>
              <span class="margin">Marge cible ${formatPrice(margin)}</span>
            </div>
            <div class="product-actions">
              <button class="add-button" type="button" data-add="${product.id}">
                Ajouter au panier
              </button>
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderCart() {
  const entries = getCartEntries();
  const totalQuantity = entries.reduce((sum, item) => sum + item.quantity, 0);
  const total = entries.reduce((sum, item) => sum + item.quantity * item.price, 0);

  cartCount.textContent = totalQuantity;
  cartTotal.textContent = formatPrice(total);

  if (!entries.length) {
    cartItems.innerHTML = '<p class="small">Ton panier est vide.</p>';
  } else {
    cartItems.innerHTML = entries
      .map(
        (item) => `
        <div class="cart-row">
          <div>
            <strong>${item.name}</strong>
            <span>${formatPrice(item.price)} x ${item.quantity}</span>
          </div>
          <div class="qty-actions">
            <button type="button" data-decrease="${item.id}" aria-label="Retirer un article">-</button>
            <strong>${item.quantity}</strong>
            <button type="button" data-add="${item.id}" aria-label="Ajouter un article">+</button>
          </div>
        </div>
      `,
      )
      .join("");
  }

  const message = [
    "Bonjour, je veux commander :",
    ...entries.map((item) => `- ${item.quantity} x ${item.name} (${formatPrice(item.price)})`),
    `Total : ${formatPrice(total)}`,
  ].join("\n");

  whatsappOrder.href = entries.length
    ? `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`
    : "#";

  saveCart();
}

function addToCart(id) {
  cart[id] = (cart[id] || 0) + 1;
  renderCart();
}

function decreaseCart(id) {
  if (!cart[id]) return;
  cart[id] -= 1;
  if (cart[id] <= 0) delete cart[id];
  renderCart();
}

function openCart() {
  cartPanel.classList.add("open");
  overlay.classList.add("open");
  cartPanel.setAttribute("aria-hidden", "false");
}

function closeCart() {
  cartPanel.classList.remove("open");
  overlay.classList.remove("open");
  cartPanel.setAttribute("aria-hidden", "true");
}

document.addEventListener("click", (event) => {
  const addButton = event.target.closest("[data-add]");
  const decreaseButton = event.target.closest("[data-decrease]");
  const filterButton = event.target.closest("[data-filter]");

  if (addButton) {
    addToCart(addButton.dataset.add);
    openCart();
  }

  if (decreaseButton) {
    decreaseCart(decreaseButton.dataset.decrease);
  }

  if (filterButton) {
    activeFilter = filterButton.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((button) => {
      button.classList.toggle("active", button === filterButton);
    });
    renderProducts();
  }

  if (event.target.closest("[data-open-cart]")) openCart();
  if (event.target.closest("[data-close-cart]")) closeCart();
});

renderProducts();
renderCart();
