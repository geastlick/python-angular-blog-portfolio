import { Component, OnInit } from '@angular/core';
import { delay } from 'rxjs/operators';
import { Blog } from 'src/app/interfaces/blog';
import { ResizeService } from 'src/app/screen-size-detector/resize.service';
import { ScreenSize } from 'src/app/screen-size-detector/screen-size';
import { BlogService } from 'src/app/services/blogs.service';

@Component({
    selector: 'app-popular-blogs',
    templateUrl: './popular-blogs.component.html',
    styleUrls: ['./popular-blogs.component.css']
})
export class PopularBlogsComponent implements OnInit {

    blogCount: number;
    blogPageSize: number = 8;
    blogPage: number = 1;
    popularBlogs: [Blog];
    rowsPerPage = [2, 4, 6, 8, 12, 16, { showAll: 'All' }];

    constructor(private blogService: BlogService, private resizeService: ResizeService) { }

    ngOnInit(): void {
        this.blogService.popular(this.blogPageSize, this.blogPage)
            .subscribe(
                result => {
                    this.blogCount = result['count_all_blogs'];
                    this.popularBlogs = result['blogs'];
                }
            );
        this.resizeService.onResize$
            .pipe(delay(0))
            .subscribe(x => {
                switch (x) {
                    case ScreenSize.XS:
                    case ScreenSize.SM:
                        this.rowsPerPage = [2, 4, 6];
                        this.paginate({ rows: 4, first: this.blogPageSize * (this.blogPage - 1) });
                        break;
                    case ScreenSize.LG:
                    case ScreenSize.MD:
                        this.rowsPerPage = [3, 6, 9];
                        this.paginate({ rows: 6, first: this.blogPageSize * (this.blogPage - 1) });
                        break;
                    default:
                        this.rowsPerPage = [4, 8, 12, { showAll: 'All' }];
                        this.paginate({ rows: 8, first: this.blogPageSize * (this.blogPage - 1) });
                        break;
                }
            });
    }

    paginate(event) {
        // page is 0 indexed
        if (event.rows != this.blogPageSize) {
            this.blogPageSize = event.rows;
            this.blogPage = Math.floor(event.first / event.rows);
            this.blogService.popular(this.blogPageSize, this.blogPage).subscribe(data => {
                this.blogCount = data['count_all_blogs'];
                this.popularBlogs = data['blogs'];
            });
        } else if (event.page + 1 != this.blogPage) {
            this.blogPage = event.page + 1;
            this.blogService.popular(this.blogPageSize, this.blogPage).subscribe(data => {
                this.blogCount = data['count_all_blogs'];
                this.popularBlogs = data['blogs'];
            });
        }
    }
}
