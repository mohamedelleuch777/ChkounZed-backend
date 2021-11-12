<?php

class MVC_App {
    function __construct () {
        $url = $_SERVER['REQUEST_URI'];
        $url = rtrim($url);
        $url = explode('/', $url);
        array_shift($url); // to remove first item because its empty

        $file = 'controllers/' . $url[0] . '.php';
        if(file_exists($file)) {
            require $file;
        } else {
            // throw new Exception("The file: $file does not exists.");
            require 'controllers/error_.php';
            $controller = new Error_();
            return;
        }

        $controller = new $url[0];

        if(isset($url[2])) {
            $this->Convert2Json($controller->{$url[1]}($url[2]));
        } else {
            /*
            if(isset($url[1])) {
                 $this->Convert2Json($controller->{$url[1]}());
            } 
            */
            $errMsg = (object)[
                'success' => false,
                'message' => "This method only accept POST",
                'request' => $_SERVER['REQUEST_METHOD'],
            ];
            $this->Convert2Json($errMsg);
        }

    }

    function Convert2Json($var) {
        $varType = gettype($var);
        if($varType=='object') {
            echo json_encode(get_object_vars($var));
        } else if($varType=='array') {
            echo json_encode($var);
        } else if($varType=='string') {
            echo '{
                "result": '.$var.'
            }';
        } else if($varType=='boolean') {
            echo '{
                "result": '.($var?"true":"false").'
            }';
        } else {
            echo "type not accepted: $varType";
        }
    }
}

?>