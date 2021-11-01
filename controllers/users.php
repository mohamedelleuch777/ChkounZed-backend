<?php

class  Users extends Controller {
    function __construct () {
        parent::__construct();
    }

    public function CreateUser() {
        $this->loadModel('m_Users');
        $users = new m_Users();
        $output = $this->ReadPostData();
        echo json_encode($output);
    }

    public function UpdateUser() {
        echo 'call Users.UpdateUser()';
    }

    public function RemoveUser() {
        echo 'call Users.RemoveUser()';
    }

    public function GetUserData() {
        echo 'call Users.GetUserData()';
    }

    private function ReadPostData() {
        $my_POST = json_decode(file_get_contents('php://input'));

        $my_POST = json_decode(json_encode($my_POST), true);
        return $my_POST;
    }
}