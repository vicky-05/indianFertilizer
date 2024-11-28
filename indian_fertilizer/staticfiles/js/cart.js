        function updateTotal() {
            let subtotal = 0;
            document.querySelectorAll('.cart-item').forEach(item => {
                const quantity = item.querySelector('.quantity').value;
                const price = parseFloat(item.querySelector('p').textContent.replace('$', ''));
                const itemTotal = quantity * price;
                item.querySelector('.item-total').textContent = `$${itemTotal.toFixed(2)}`;
                subtotal += itemTotal;
            });

            const tax = subtotal * 0.05; // Assuming 5% tax rate
            const total = subtotal + tax;
            document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
            document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
            document.getElementById('total').textContent = `$${total.toFixed(2)}`;
        }

        function removeItem(button) {
            const item = button.closest('.cart-item');
            item.remove();
            updateTotal();
        }

        function checkCartStatus() {
            const cartItems = document.querySelectorAll('.cart-item:not(.d-none)').length;
            if (cartItems === 0) {
                document.getElementById('emptyCartMessage').classList.remove('d-none');
                document.getElementById('cartItems').classList.add('d-none');
                document.getElementById('cartSummary').classList.add('d-none');
            }
        }

        // Initial check for empty cart status
        checkCartStatus();