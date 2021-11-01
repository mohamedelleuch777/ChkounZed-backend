<?php 

class Controller {
    function __construct () {
        // echo 'Virtual controller has been called <br/>';
    }

    public function loadModel($modelName) {
        require "models/$modelName.php";
    }
}