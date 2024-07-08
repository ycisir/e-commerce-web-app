$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Get all info messages
var info_messages = document.getElementsByClassName('alert');

setTimeout(function(){
    for (var i = 0; i < info_messages.length; i ++) {
        // Set display attribute as !important, neccessary when using bootstrap
        info_messages[i].setAttribute('style', 'display:none !important');
    }
}, 3000);


$('.plus-cart').click(function (){
    var id = $(this).attr('pid').toString();
    var elm = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        typr:'GET',
        url:'/plus-cart',
        data:{
            product_id:id
        },
        success: function(data){
            elm.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})


$('.minus-cart').click(function (){
    var id = $(this).attr('pid').toString();
    var elm = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        typr:'GET',
        url:'/minus-cart',
        data:{
            product_id:id
        },
        success: function(data){
            elm.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})


$('.remove-cart').click(function (){
    var id = $(this).attr('pid').toString();
    var elm = this
    // console.log(id)
    $.ajax({
        typr:'GET',
        url:'/remove-cart',
        data:{
            product_id:id
        },
        success: function(data){
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
            elm.parentNode.parentNode.parentNode.parentNode.remove()
            document.getElementById('msg').innerText = data.msg
            document.getElementById('badge').innerText = data.items
            // console.log(data.msg)
        }
    })
})



function ShowFunction() {
    var opw = document.getElementById("oldpwd");
    var pw1 = document.getElementById("password1");
    var pw2 = document.getElementById("password2");
    if ((pw1.type || pw2.type || opw.type) === "password") {
        // console.log('hi working')
        pw1.type = "text";
        pw2.type = "text";
        opw.type = "text";
    } else {
      pw1.type = "password";
      pw2.type = "password";
      opw.type = "password";
    }
} 


(function () {
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };
})();