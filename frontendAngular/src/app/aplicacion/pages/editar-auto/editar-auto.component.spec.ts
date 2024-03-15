import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditarAutoComponent } from './editar-auto.component';

describe('EditarAutoComponent', () => {
  let component: EditarAutoComponent;
  let fixture: ComponentFixture<EditarAutoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditarAutoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditarAutoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
