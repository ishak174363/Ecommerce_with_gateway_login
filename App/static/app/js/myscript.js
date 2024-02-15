// Add to cart
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    console.log("pid=",id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

//minus from cart
$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


//remove cart
$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})


//plus wishlist
$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist/",
        data: {
            prod_id: id
        },
        success: function(data){
            if (data.message === 'Added to wishlist') {
                alert("Added to wishlist");
                // Handle redirection or UI update as needed
            } else {
                alert("Failed to add to wishlist");
            }
        }
    })
});

//minus wishlist
$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist/",
        data: {
            prod_id: id
        },
        success: function(data){
            if (data.message === 'Removed from wishlist') {
                alert("Removed from wishlist");
                // Handle redirection or UI update as needed
            } else {
                alert("Failed to remove from wishlist");
            }
        }
    })
});
