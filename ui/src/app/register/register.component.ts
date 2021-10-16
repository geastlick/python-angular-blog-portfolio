import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { UserService } from '../services/users.service';

@Component({
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

    @Output() private status = new EventEmitter<any>();

    registerForm = new FormGroup({
        username: new FormControl(''),
        password: new FormControl(''),
        password_confirm: new FormControl(''),
        name: new FormControl(''),
        email: new FormControl(''),
    })

    constructor(private userService: UserService) { }

    ngOnInit(): void { }

    handleCancel(): void {
        this.status.emit({ action: "Cancelled" });
    }

    handleRegister(): void {
        this.userService.register(this.registerForm.get('username').value, this.registerForm.get('password').value, this.registerForm.get('name').value, this.registerForm.get('email').value)
            .subscribe(
                result => {
                    if (result.error != undefined) {
                        switch (result.error) {
                            case "Duplicate username":
                                this.status.emit("Register Username");
                                break;
                            case "Duplicate email":
                                this.status.emit("Register Email");
                                break;
                            default:
                                this.status.emit("Register Failure");
                                break;
                        }
                    } else if (result.success != undefined) {
                        this.status.emit("Register Success");
                    } else this.status.emit("Register Failure");
                }
            );

    }

}
