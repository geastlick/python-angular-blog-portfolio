import { Injectable } from '@angular/core';

@Injectable()
export class ErrorMessageService {
    messages: string[] = [];

    add(message: string) {
        this.messages.push(message);
    }

    clear() {
        this.messages = [];
    }
}

