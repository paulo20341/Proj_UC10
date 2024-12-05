document.addEventListener('DOMContentLoaded', function() {
    const productGrid = document.getElementById('productGrid');
    const products = [
        { name: "Cama Pet Luxo", price: 149.99, images: ["cama1.png"], description: "Cama aconchegante para seu gato." },
        { name: "Almofada Para Gato", price: 59.99, images: ["almo.png"], description: "Almofada macia para sonecas." }
    ];

    function createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.images[0]}" alt="${product.name}" class="product-image">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>R$ ${product.price.toFixed(2)}</p>
            <button class="buy-btn">Comprar</button>
        `;
        return card;
    }

    products.forEach(product => {
        productGrid.appendChild(createProductCard(product));
    });
});
