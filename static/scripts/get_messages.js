function retrieveMessages(url) {
    jQuery.ajax({
        type: "GET",
        url: "/check_for_messages",
        contentType: "application/json",
        data: {"walletAddress": window.userWalletAddress},
        dataType: "json",
        success: function(response) {
            console.log(response)
            if (response.success == true){
                window.location = "/"+url+"/"+response.data;
            }
        }
    })
}