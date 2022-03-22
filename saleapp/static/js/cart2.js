var cartCounter = document.getElementById('cart__counter')
var cartCounter2 = document.getElementById('cart__counter-2')
var cartAmounts = document.getElementsByClassName('cart__amount')

function addToCart(id, name, price, image) {
    event.preventDefault()
    // promise
    fetch('/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'image': image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        // console.log(data)
        
        cartCounter.innerText = data.total_quantity
    })
    .catch(err => console.error(err))
};

function updateCart(obj, id) {
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            id: id,
            quantity: parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(res => {
        cartCounter.innerText = res.data.total_quantity
        cartCounter2.innerText = res.data.total_quantity
        
        cartAmounts.forEach(cartAmount => {
            cartAmount.innerText = new Intl.NumberFormat().format(res.data.total_amount) + " VND"
        })
    }) 
    .catch(err => console.error(err))
};


function deleteCart(obj, id) {
    event.preventDefault()

    if (confirm('Ban chac chan muon xoa khong?') == true) {
        fetch('/api/delete-cart', {
            method: 'delete',
            body: JSON.stringify({
                id: id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(res => {
            if (res.code == 200) {
                cartCounter.innerText = res.data.total_quantity
                cartCounter2.innerText = res.data.total_quantity
                
                cartAmounts.forEach(cartAmount => {
                    cartAmount.innerText = new Intl.NumberFormat().format(res.data.total_amount) + " VND"
                })

                var parent = obj.closest(`#cart-${id}`)
                parent.remove()
            }
        }) 
        .catch(err => console.error(err))
        
    }
};


function pay() {
    event.preventDefault()
    
    if (confirm('Ban chac chan thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        })
        .then(res => res.json())
        .then(data => {
            if (data.code === 200)
            location.reload()
        })
        .catch(err => console.error(err))
    }
};