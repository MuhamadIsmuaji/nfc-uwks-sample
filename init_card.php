<?php

$f = popen('python /var/www/nfcuwks/python_script/read_card.py', 'r');
if ($f === false) {
   echo "popen failed";
}

$json = fgets($f);

echo $json;

fclose($f);