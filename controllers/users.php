<?php

class  Users extends Controller {
    function __construct () {
        parent::__construct();
    }

    public function CreateUser() {
        echo 'call Users.CreateUser()';
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
}