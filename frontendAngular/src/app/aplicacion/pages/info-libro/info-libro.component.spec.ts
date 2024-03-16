import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoLibroComponent } from './info-libro.component';

describe('InfoLibroComponent', () => {
  let component: InfoLibroComponent;
  let fixture: ComponentFixture<InfoLibroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InfoLibroComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InfoLibroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
