<!DOCTYPE html>
<html>
<head>
	<title>Coba Bro</title>
</head>
	<script type="text/javascript" src="assets/jquery.min.js"></script>
<body>
	Status : <input type="text" name="status" id="status" > <br/>
	Npm : <input type="text" name="npm" id="npm" > <br/>

	<script type="text/javascript">

		var read = 0;
		
		$(function() {

			var refresh = setInterval(function(){
				$.ajax({
					'url' : 'init.php',
					'type' : 'POST',
					'dataType' : 'JSON'
				})
				.done(function(response){
					$('#status').val(response.message)

					if (response.status == "3") {
						// console.log(response)
						readCard()
					} else {
						read = 0;
						$('#npm').val('');
					}

				})
				.fail(function(jqXHR, textStatus, errorThrown){
					console.log('Error : '+ jqXHR.responseText);
				});

				// console.log("a");
			},1000);

		});

		function readCard() {
			if (read != 1) {
				$.ajax({
					'url' : 'init_card.php',
					'type' : 'POST',
					'dataType' : 'JSON'
				})
				.done(function(response){
					$('#npm').val(response.npm)
					read = 1;
					// console.log(response)

					// reader_status = response.status;
				})
				.fail(function(response){
					console.log('Error : '+ jqXHR.responseText);
				});
			} 
		}


	</script>
</body>
</html>