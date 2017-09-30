<?php

$f = popen('python python_script/own_reader.py', 'r');
if ($f === false) {
    echo "popen failed";
}

$json = fgets($f);

echo $json;

fclose($f);
