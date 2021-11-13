<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$requestType = $_SERVER['REQUEST_METHOD'];
$postData = json_encode(json_decode(file_get_contents('php://input')));
file_put_contents("php.input",$postData);
$urlpath = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
$urlParameters = $_SERVER['QUERY_STRING'];
$res = exec("python3 index.py $requestType $urlpath \"$urlParameters\"");
echo $res; 
