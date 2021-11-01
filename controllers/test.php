<?php

class Test extends Controller {
    function __construct() {
        parent::__construct();
        echo "hello world'!!!<br />";
    }

    public function hi() {
        echo 'this is the hi method executed!!!';
    }

    public function exec() {
        $output = $this->ReadPostData();
        echo json_encode($output);
    }

    private function ReadPostData() {
        $my_POST = json_decode(file_get_contents('php://input'));

        $my_POST = json_decode(json_encode($my_POST), true);
        return $my_POST;
    }
}