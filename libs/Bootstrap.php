<?php

class Bootstrap {
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
            $controller->{$url[1]}($url[2]);
        } else {
            if(isset($url[1])) {
                $controller->{$url[1]}();
            }
        }

    }
}

?>