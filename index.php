<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$requestType = $_SERVER['REQUEST_METHOD'];
$postData = json_encode(json_decode(file_get_contents('php://input')));
file_put_contents("php.input",$postData);
$url = $_SERVER['REQUEST_URI'];
$res = exec("python3 index.py $requestType $url");
echo $res; 
