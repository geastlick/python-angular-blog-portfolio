import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { distinctUntilChanged } from 'rxjs/operators';
import { ScreenSize } from './screen-size';

@Injectable({
    providedIn: 'root'
})
export class ResizeService {

    size: ScreenSize;

    get onResize$(): Observable<ScreenSize> {
        return this.resizeSubject.asObservable().pipe(distinctUntilChanged());
    }

    private resizeSubject: Subject<ScreenSize>;

    constructor() {
        this.resizeSubject = new Subject();
    }

    onResize(size: ScreenSize) {
        this.size = size;
        this.resizeSubject.next(size);
    }
}
