import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
    selector: 'app-signin-register',
    templateUrl: './signin-register.component.html',
    styleUrls: ['./signin-register.component.css']
})
export class SigninRegisterComponent implements OnInit {

    @Input() display: boolean = false;
    @Output() result = new EventEmitter();

    constructor() { }

    ngOnInit(): void {
    }

    onSigninStatus(result) {
        this.result.emit(result)
    }

    onRegisterStatus(result) {
        this.result.emit(result)
    }

}
