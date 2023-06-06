using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Models
{
    public class Movimientos
    {
        public int Id { get; set; }
        public int PuntosId { get; set; }
        public int ModoId { get; set; }
        public DateTime? Fecha { get; set; }
    }
}
