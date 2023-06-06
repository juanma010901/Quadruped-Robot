using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Models
{
    public class Modos
    {
        public int Id { get; set; }

        public bool Activo { get; set; }
        public string Descripcion { get; set; }
        public int SeccionId { get; set; }
        public DateTime? Fecha { get; set; }
    }
}
