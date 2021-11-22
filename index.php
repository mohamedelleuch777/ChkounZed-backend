<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$requestType = $_SERVER['REQUEST_METHOD'];
$postData = json_encode(json_decode(file_get_contents('php://input')));
file_put_contents("php.input",$postData);
$urlpath = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
$urlParameters = '';
if(isset($_SERVER['QUERY_STRING'])){
    $urlParameters = $_SERVER['QUERY_STRING'];
}
$jsonServerData = json_encode($_SERVER);
file_put_contents("headers.input",$jsonServerData);
$res = exec("python3 index.py $requestType $urlpath \"$urlParameters\"");
//var_dump($res);die;
$statusCode = (int)substr($res,0,3);
$reply = substr($res,3);
http_response_code($statusCode);
echo $reply; 
