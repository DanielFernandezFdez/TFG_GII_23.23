import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EstimacionesGuardadasComponent } from './estimaciones-guardadas.component';

describe('EstimacionesGuardadasComponent', () => {
  let component: EstimacionesGuardadasComponent;
  let fixture: ComponentFixture<EstimacionesGuardadasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EstimacionesGuardadasComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EstimacionesGuardadasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
