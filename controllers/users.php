<?php

class  Users extends Controller {
    function __construct () {
        parent::__construct();
    }

    public function CreateUser() {
        $this->loadModel('m_Users');
        $users = new m_Users();
        $output = $this->Post();
        return $users->CreateUser($output);
    }

    public function UpdateUser() {
        echo 'call Users.UpdateUser()';
    }

    public function RemoveUser() {
        echo 'call Users.RemoveUser()';
    }

    public function GetUser() {
        $this->loadModel('m_Users');
        $users = new m_Users();
        $output = $this->Post();
        //echo json_encode($output);
        return $users->GetUserByEmail($output);
    }
}