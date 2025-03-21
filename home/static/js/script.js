document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            const itemName = encodeURIComponent(this.getAttribute("data-name"));
            const itemPrice = encodeURIComponent(this.getAttribute("data-price"));

            fetch(`/add-to-cart/?name=${itemName}&price=${itemPrice}`)
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    document.getElementById("cart-count").innerText = data.cart_count;
                    alert("Item added to cart!");
                } else if (data.error) {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});




