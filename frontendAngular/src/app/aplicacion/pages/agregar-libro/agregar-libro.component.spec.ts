import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgregarLibroComponent } from './agregar-libro.component';

describe('AgregarLibroComponent', () => {
  let component: AgregarLibroComponent;
  let fixture: ComponentFixture<AgregarLibroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AgregarLibroComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgregarLibroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
