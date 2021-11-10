<?php 

class Controller {
    function __construct () {
        // echo 'Virtual controller has been called <br/>';
    }

    public function loadModel($modelName) {
        require "models/$modelName.php";
    }

    public function GetRequestType() {
        return $_SERVER['REQUEST_METHOD'];
    }

    public function Post() {
        $req = $this->GetRequestType();
        if($req!='POST') {
            die ('{
                "success": false,
                "message": "This method only accept POST",
                "request": "'.$req.'"
            }');
        }
        $my_POST = json_decode(file_get_contents('php://input'));

        $my_POST = json_decode(json_encode($my_POST), true);
        return $my_POST;
    }
}