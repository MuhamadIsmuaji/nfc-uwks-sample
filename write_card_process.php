<?php

$statusnya = $_POST['status'];

$f = popen('python /var/www/nfcuwks/python_script/write_card.py '. $statusnya, 'r');

if ($f === false) {
   echo "popen failed";
}

$json = fgets($f);

echo $json;

fclose($f);