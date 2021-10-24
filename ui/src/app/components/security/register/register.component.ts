import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl, Validators, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { UserService } from '../../../services/users.service';


export const passwordsMustMatch: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const pwd = control.get('password');
    const confirm = control.get('password_confirm');
  
    return pwd && confirm && pwd.value === confirm.value ? { passwordsMustMatch: true } : null;
  };

@Component({
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

    @Output() private status = new EventEmitter<any>();

    registerForm = new FormGroup({
        username: new FormControl('', [ 
            Validators.required,
            Validators.minLength(3)
        ]),
        password: new FormControl('', [
            Validators.required,
            Validators.minLength(8)
        ]),
        password_confirm: new FormControl('', [
            Validators.required
        ]),
        name: new FormControl('', [
            Validators.required
        ]),
        email: new FormControl('', [
            Validators.required,
            Validators.email
        ]),
    }, { validators: passwordsMustMatch})

    get username() { return this.registerForm.get('username'); }
    get password() { return this.registerForm.get('password'); }
    get password_confirm() { return this.registerForm.get('password_confirm'); }
    get name() { return this.registerForm.get('name'); }
    get email() { return this.registerForm.get('email'); }

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
