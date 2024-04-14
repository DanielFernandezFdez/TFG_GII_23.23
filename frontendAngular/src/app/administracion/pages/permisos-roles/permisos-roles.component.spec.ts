import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PermisosRolesComponent } from './permisos-roles.component';

describe('PermisosRolesComponent', () => {
  let component: PermisosRolesComponent;
  let fixture: ComponentFixture<PermisosRolesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PermisosRolesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PermisosRolesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
