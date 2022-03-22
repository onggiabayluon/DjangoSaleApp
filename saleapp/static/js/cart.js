var updateBtns = document.getElementsByClassName('update-cart');
var updateQuantityBtns = document.getElementsByClassName('update-cart-quantity');
var cartCounter = document.getElementById('cart__counter')
var cartCounter2 = document.getElementById('cart__counter-2')
var cartAmount = document.getElementById('cart__amount')
var update_item_url = '/shopping/update_item/'
var delete_item_url = '/shopping/delete_item/'
var update_item_quantity_url = '/shopping/update_item_quantity/'


for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
       
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateUserOrder(productId, action)
        }

    })
}

function updateUserOrder(productId, action) {
    fetch(update_item_url, {
        method: 'post',
        body: JSON.stringify({
            'productId': productId,
            'action': action
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(data => {
        // console.log(data)
        cartCounter.innerText = data.cart_count
    })
}


function updateItemQuantity(obj, productId) {
    fetch(update_item_quantity_url, {
        method: 'post',
        body: JSON.stringify({
            'productId': productId,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
        .then(res => res.json())
        .then(data => {
            cartCounter.innerText = data.cart_count
            cartCounter2.innerText = data.cart_count
            let item_price = document.getElementById(`product-price-${productId}`)
            item_price.innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.item_total)
            cartAmount.innerHTML = "$" + data.cart_total
        })
}


function deleteCartItem(obj, productId) {
    event.preventDefault()
    
    if (confirm('Ban chac chan muon xoa khong?') == true) {
        fetch(delete_item_url, {
            method: 'post',
            body: JSON.stringify({
                'productId': productId,
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })
        .then(res => res.json())
        .then(data => {
            cartCounter.innerText = data.cart_count
            cartCounter2.innerText = data.cart_count
            let item_price = document.getElementById(`product-price-${productId}`)
            item_price.innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.item_total)
            cartAmount.innerHTML = "$" + data.cart_total

            var parent = obj.closest(`#cart-${productId}`)
            parent.remove()
        })
    }

}