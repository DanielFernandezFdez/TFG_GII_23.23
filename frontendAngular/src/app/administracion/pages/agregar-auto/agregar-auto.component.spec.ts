import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgregarAutoComponent } from './agregar-auto.component';

describe('AgregarAutoComponent', () => {
  let component: AgregarAutoComponent;
  let fixture: ComponentFixture<AgregarAutoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AgregarAutoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgregarAutoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
