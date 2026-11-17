from sqlalchemy.orm import Session
from sqlalchemy import text

class EmpleadoCitasRepository:
    def obtener_citas_por_empleado(self, db: Session, empleado_id: int) -> list:
        """
        Consulta las citas asignadas a la manicurista/empleado específico.
        Nota: Ajusta los nombres de las tablas y columnas según tu modelo real de base de datos de reservas/citas.
        """
        query = text("""
            SELECT r.id AS id_reserva, 
                   c.nombre AS cliente, 
                   r.hora_inicio, 
                   s.nombre AS servicio, 
                   r.modalidad
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id
            JOIN servicios s ON r.servicio_id = s.id
            WHERE r.empleado_id = :empleado_id AND r.estado = 'Programada'
        """)
        
        resultado = db.execute(query, {"empleado_id": empleado_id}).fetchall()
        
        # Mapear a diccionarios limpios
        citas = []
        for row in resultado:
            citas.append({
                "id_reserva": row.id_reserva,
                "cliente": row.cliente,
                "hora_inicio": str(row.hora_inicio),
                "servicio": row.servicio,
                "modalidad": row.modalidad
            })
        return citas