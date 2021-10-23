import { Component, OnInit } from '@angular/core';
import { Blog } from 'src/app/interfaces/blog';
import { BlogService } from 'src/app/services/blogs.service';
import { PageOptionIndex } from '../custom/responsive-paginator/page-option-index';
import { PageOptions } from '../custom/responsive-paginator/page-options';
import { PaginatorPageChange } from '../custom/responsive-paginator/paginator-page-change';

@Component({
    selector: 'app-popular-blogs',
    templateUrl: './popular-blogs.component.html',
    styleUrls: ['./popular-blogs.component.css']
})
export class PopularBlogsComponent implements OnInit {

    itemCount: number;
    popularBlogs: [Blog];

    pageOptionIndex: PageOptionIndex = { screenSize: 'MD', index: 1 };
    pageOptions: PageOptions = [];
    initialPage: number = 1;

    constructor(private blogService: BlogService) { }

    ngOnInit(): void {
        this.pageOptions['SM'] = [2, 4, 6, { showAll: 'All' }];
        this.pageOptions['MD'] = [3, 6, 9, { showAll: 'All' }];
        this.pageOptions['XL'] = [4, 8, 12, { showAll: 'All' }];
    }

    onPageChange(event: PaginatorPageChange) {
        this.blogService.popular(event.pageSize, event.page).subscribe(data => {
            this.itemCount = data['count_all_blogs'];
            this.popularBlogs = data['blogs'];
        });

    }

}
