import { Component, AfterViewInit, HostListener, ElementRef } from '@angular/core';
import { ResizeService } from './resize.service';
import { ScreenSize } from './screen-size';


@Component({
    selector: 'app-size-detector',
    templateUrl: './size-detector.component.html',
    styleUrls: ['./size-detector.component.css']
})
export class SizeDetectorComponent implements AfterViewInit {

    prefix = 'is-';
    sizes = [
        {
            id: ScreenSize.XS, name: 'xs', css: 'block sm:hidden'
        },
        {
            id: ScreenSize.SM, name: 'sm', css: 'hidden sm:block md:hidden'
        },
        {
            id: ScreenSize.MD, name: 'md', css: 'hidden md:block lg:hidden'
        },
        {
            id: ScreenSize.LG, name: 'lg', css: 'hidden lg:block xl:hidden'
        },
        {
            id: ScreenSize.XL, name: 'xl', css: 'hidden xl:block'
        },
    ];

    constructor(private elementRef: ElementRef, private resizeSvc: ResizeService) { }

    @HostListener("window:resize", [])
    private onResize() {
        this.detectScreenSize();
    }

    ngAfterViewInit() {
        this.detectScreenSize();
    }

    private detectScreenSize() {
        const currentSize = this.sizes.find(x => {
            const el = this.elementRef.nativeElement.querySelector(`.${this.prefix}${x.id}`);
            const isVisible = window.getComputedStyle(el).display != 'none';

            return isVisible;
        });

        this.resizeSvc.onResize(currentSize.id);
    }
}
