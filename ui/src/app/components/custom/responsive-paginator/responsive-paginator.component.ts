import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ResizeService } from 'src/app/screen-size-detector/resize.service';
import { ScreenSize } from 'src/app/screen-size-detector/screen-size';
import { delay } from 'rxjs/operators';
import { PageOptionIndex } from 'src/app/components/custom/responsive-paginator/page-option-index';
import { PageOptions } from 'src/app/components/custom/responsive-paginator/page-options';
import { PaginatorPageChange } from './paginator-page-change';

@Component({
    selector: 'app-responsive-paginator',
    templateUrl: './responsive-paginator.component.html',
    styleUrls: ['./responsive-paginator.component.css']
})
export class ResponsivePaginatorComponent implements OnInit {

    @Input() pageOptionIndex: PageOptionIndex;
    @Input() pageOptions: PageOptions;
    @Input() initialPage: number;
    @Input() itemCount: number;
    @Output() onPageChange: EventEmitter<PaginatorPageChange> = new EventEmitter();

    currentPage: number = 1;

    currentPageSize: number;
    rowsPerPageOption;

    constructor(private resizeService: ResizeService) { }

    ngOnInit(): void {
        this.rowsPerPageOption = this.pageOptions[this.pageOptionIndex.screenSize];
        this.currentPageSize = this.rowsPerPageOption[this.pageOptionIndex.index];
        this.resizeService.onResize$
            .pipe(delay(0))
            .subscribe(x => {
                this.configure(x);
            });
        this.configure(this.resizeService.size);
    }

    findSizeOption(size: ScreenSize): string {
        let defaultSize: string = "";
        if ('XS' in this.pageOptions) { defaultSize = 'XS'; }
        if (size == ScreenSize.XS && defaultSize != "") { return defaultSize; }
        if ('SM' in this.pageOptions) { defaultSize = 'SM'; }
        if (size in [ScreenSize.XS, ScreenSize.SM] && defaultSize != "") { return defaultSize; }
        if ('MD' in this.pageOptions) { defaultSize = 'MD'; }
        if (size in [ScreenSize.XS, ScreenSize.SM, ScreenSize.MD] && defaultSize != "") { return defaultSize; }
        if ('LG' in this.pageOptions) { defaultSize = 'LG'; }
        if (size in [ScreenSize.XS, ScreenSize.SM, ScreenSize.MD, ScreenSize.LG] && defaultSize != "") { return defaultSize; }
        if ('XL' in this.pageOptions) { defaultSize = 'XL'; }
        return defaultSize;
    }

    configure(size: ScreenSize) {
        let index = (this.currentPageSize == this.itemCount ? this.rowsPerPageOption.length - 1 : this.rowsPerPageOption.indexOf(this.currentPageSize));
        let sizeOption = this.findSizeOption(size);
        this.rowsPerPageOption = this.pageOptions[sizeOption];
        this.paginate({ rows: (this.currentPageSize == this.itemCount ? this.itemCount : this.rowsPerPageOption[index]), first: this.currentPageSize * (this.currentPage - 1) });
    }

    paginate(event) {
        // page is 0 indexed
        if (event.rows != this.currentPageSize) {
            this.currentPageSize = event.rows;
            this.currentPage = Math.floor(event.first / event.rows);
            this.onPageChange.emit({ pageSize: this.currentPageSize, page: this.currentPage })
        } else if (event.page + 1 != this.currentPage) {
            this.currentPage = event.page + 1;
            this.onPageChange.emit({ pageSize: this.currentPageSize, page: this.currentPage })
        }
    }

}
