<!DOCTYPE html>
<html>
<head>
	<title>Coba write status</title>

	<script type="text/javascript" src="assets/jquery.min.js"></script>

</head>
<body>
	<form id="formcoba" name="formcoba">
		Status Anggota Perpustakaan : <br>
			<input type="radio" name="status" value="1" checked> Aktif<br>
			<input type="radio" name="status" value="0"> Tidak Aktif<br>

		Status Write
			<input type="text" name="write_status" id="write_status" value="No status" /> <br>
	</form>

	<button id="simpan" name="simpan">Simpan</button>

	<script type="text/javascript">
		
		$(function(){

			$('#simpan').on('click', function(){

				$('#write_status').val('Mohon tunggu...');

				$.ajax({
					'url' : 'write_card_process.php',
					'type' : 'POST',
					'data' : $('#formcoba').serialize(),
					'dataType' : 'JSON'
				})
				.done(function(response){
					$('#write_status').val(response.write);					
				})
				.fail(function(jqXHR, textStatus, errorThrown){
					console.log('Error : '+ jqXHR.responseText);
				});
			});
		});


	</script>
</body>
</html>