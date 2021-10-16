import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { UserService } from '../../../services/users.service';

@Component({
    selector: 'app-signin',
    templateUrl: './signin.component.html',
    styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {

    @Output() private status = new EventEmitter<any>();

    signinForm = new FormGroup({
        username: new FormControl(''),
        password: new FormControl(''),
    })

    constructor(private userService: UserService) { }

    ngOnInit(): void { }

    handleCancel(): void { 
        this.status.emit({action: "Cancelled"});
    }

    handleSignIn(): void {
        this.userService.login(this.signinForm.get('username').value, this.signinForm.get('password').value)
            .subscribe(
                result => {
                    this.status.emit((result ? "Log In Success" : "Log In Failure"))
                }
            );
    }

}
