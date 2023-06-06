using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Models
{
    public class Puntos
    {
        public int Id { get; set; }
        public int P1X { get; set; }
        public int P1Y { get; set; }
        public int P2X { get; set; }
        public int P2Y { get; set; }
        public int P3X { get; set; }
        public int P3Y { get; set; }
        public int P4X { get; set; }
        public int P4Y { get; set; }
        public DateTime? Fecha { get; set; }

    }
}
